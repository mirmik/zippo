#include <crow/pubsub.h>
#include <crow/gates/udpgate.h>

#include <gxx/print/stdprint.h>

#include <gxx/math/madgwick.h>
#include <gxx/math/linalg.h>
#include <gxx/print/linalg.h>
#include <gxx/util/hexer.h>

#include <thread>
#include <chrono>

namespace cstd {
	template<class T, class Compare>
	constexpr const T& clamp( const T& v, const T& lo, const T& hi, Compare comp )
	{
   		return comp(v, lo) ? lo : comp(hi, v) ? hi : v;
	}

	template<class T>
	constexpr const T& clamp( const T& v, const T& lo, const T& hi )
	{
	    return clamp( v, lo, hi, std::less<>() );
	}
}

using namespace linalg::aliases;
using namespace linalg;

Madgwick ahrs;
bool coralg ;

volatile bool enabledata = false;

float3 eg(0.0);
float3 zgyr(-0.015,0.013,0.001);

int count = 0;

float p;
float r;
float y;

void mhandler(crow::packet* pack) {
	enabledata = true;

	float alpha = 0;
	float4 lq;
	float4 q;

	auto data = crow::pubsub::get_data(pack);

	if (count < 500) {
		count++;
	}
	else if (count < 600) {
		ahrs.setKoeff(50, 0.5);
		alpha = 0.05;
		count++;
	} else {
		alpha = 0.05;
	}

	//Размечаем данные в пакете.
	float3& acc = * (float3*) &data[0];
	float3& gyr = * (float3*) &data[12];
	float3& mag = * (float3*) &data[24];

    float3 corgyr = gyr - zgyr;

    float glen2 = length2(corgyr);

	//Запоминаем текущее состояние.
	ahrs.readQuaternions(&lq.w,&lq.x,&lq.y,&lq.z);

	//Применяем новые данные.
	if (glen2 < 1) {
		ahrs.update(corgyr[0], corgyr[1], corgyr[2], acc[0], acc[1], acc[2], mag[0], mag[1], mag[2]);
		coralg =  true;
	}
	else {
		ahrs.update(corgyr[0], corgyr[1], corgyr[2]);
		coralg =  false;
	}
	
	//Запоминаем вычисленное состояние.
	ahrs.readQuaternions(&q.w,&q.x,&q.y,&q.z);

	//Вычисляем углы в интересующей нас системе координат.
	ahrs.getRotZYZ(&y, &p, &r);

	//auto qdiff = normalize( qmul(q, qinv(lq)) );

	auto qdiff = float4(1.0 / (1.0/(50))) * (q - lq);
    auto ww = float4(2) * qmul(qdiff, qinv(lq));
    auto w = qrot(qinv(lq), ww.xyz());

    ahrs.getRotZYZ(&y, &p, &r);

	crow::release(pack);
}

#define MAXSIG 0.6

void publish_thread() {
	while(1) {
		if (enabledata) {
			float summ = - (p * RAD_TO_DEG - 50.0) / 40.0 * MAXSIG;
			float diff = (r * RAD_TO_DEG) / 90.0 * MAXSIG;
	
	
			float data[2];
			data[0] = summ - diff;//(diff > 0 ? diff : 0);
			data[1] = summ + diff;//(diff < 0 ? diff : 0);
	
			data[0] = cstd::clamp<float>(data[0], -MAXSIG, MAXSIG);
			data[1] = cstd::clamp<float>(data[1], -MAXSIG, MAXSIG);

			printf("kv0:%7.3f kv1:%7.3f   \n", data[0], data[1]);
	
			const char* thm = "zippo_control";
			crow::publish_buffer(thm, (const char*)data, 8, 0, 200);
			enabledata = false;
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}
}

int main() {
	uint8_t _raddr[20];

	ahrs.reset();
	ahrs.setKoeff(50, 0.5);

	const char * raddr = ".12.127.0.0.1:10009"; 
	int rlen = hexer(_raddr, 20, raddr, strlen(raddr));

	crow::set_publish_host(_raddr, rlen);
	crow::subscribe("ahrs", 0, 200);

	crow::create_udpgate(9999, 12);

	crow::pubsub_handler = mhandler;

	auto thr = std::thread(publish_thread);
	thr.detach();

	crow::spin();
}
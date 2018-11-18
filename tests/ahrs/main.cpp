#include <crow/pubsub.h>
#include <crow/gates/udpgate.h>

#include <gxx/print/stdprint.h>

#include <gxx/math/madgwick.h>
#include <gxx/math/linalg.h>
#include <gxx/print/linalg.h>
#include <gxx/util/hexer.h>

#include <thread>
#include <chrono>
//#include <algorithm>

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
//float2 kvec_x(-0.015, 0);
//float2 kvec_y(0.013, 0);
//float2 kvec_z(0.001, 0);
  

float3 zgyr(-0.015,0.013,0.001);

int count = 0;

float p;
float r;
float y;

void mhandler(crowket* pack) {
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

    /*auto error_model_x = float2(1, gyr.x - kvec_x[0]);
    auto error_model_y = float2(1, gyr.y - kvec_y[0]);
    auto error_model_z = float2(1, gyr.z - kvec_z[0]);*/

    float3 corgyr = gyr - zgyr;

    float glen2 = length2(corgyr);

	//Запоминаем текущее состояние.
	ahrs.readQuaternions(&lq.w,&lq.x,&lq.y,&lq.z);

	//Применяем новые данные.
	//ahrs.update(gyr[0] - kvec_x, gyr[1] - kvec_y, gyr[2] - kvec_z, 
	if (glen2 < 1) {
		ahrs.update(corgyr[0], corgyr[1], corgyr[2], acc[0], acc[1], acc[2], mag[0], mag[1], mag[2]);
		coralg =  true;
	}
	else {
		ahrs.update(corgyr[0], corgyr[1], corgyr[2]);
		coralg =  false;
	}
	
	//ahrs.update(gyr[0], gyr[1], gyr[2], acc[0], acc[1], acc[2]);
	
	//Запоминаем вычисленное состояние.
	ahrs.readQuaternions(&q.w,&q.x,&q.y,&q.z);



	//Вычисляем углы в интересующей нас системе координат.
	ahrs.getRotZYZ(&y, &p, &r);

	//auto qdiff = normalize( qmul(q, qinv(lq)) );

	auto qdiff = float4(1.0 / (1.0/(50))) * (q - lq);
    auto ww = float4(2) * qmul(qdiff, qinv(lq));
    auto w = qrot(qinv(lq), ww.xyz());

    //eg = /*eg +*/ (gyr - w /*- eg*/) /** float3(0.004)*/;


    /*auto E_x = dot(error_model_x, kvec_x);
    auto e_x = gyr.x - w.x;

    auto E_y = dot(error_model_y, kvec_y);
    auto e_y = gyr.y - w.y;

    auto E_z = dot(error_model_z, kvec_z);
    auto e_z = gyr.z - w.z;


    //gxx::println(E, e);
    kvec_x[1] = kvec_x[1] + normalize(error_model_x)[1] * float2(e_x - E_x)[1] * alpha;
    kvec_y[1] = kvec_y[1] + normalize(error_model_y)[1] * float2(e_y - E_y)[1] * alpha;
    kvec_z[1] = kvec_z[1] + normalize(error_model_z)[1] * float2(e_z - E_z)[1] * alpha;
*/

    //gxx::println(w);

	//qdiff = qmul(qdiff, lq);

    ahrs.getRotZYZ(&y, &p, &r);

	/*float restorekoeff = 50 * 2;

	printf("x:%7.3f y:%7.3f z:%7.3f    ", qdiff.x * restorekoeff, qdiff.y * restorekoeff, qdiff.z * restorekoeff);
	//printf("x:%7.3f y:%7.3f z:%7.3f    ", qdiff.x, qdiff.y, qdiff.z);
	*/
	//printf("gx:%7.3f gy:%7.3f gz:%7.3f    ", gyr[0], gyr[1], gyr[2]);
	//printf("wx:%7.3f wy:%7.3f wz:%7.3f    ", w.x, w.y, w.z);
	//printf("egx:%7.3f egy:%7.3f egz:%7.3f    ", eg.x, eg.y, eg.z);
	//printf("qw:%7.3f qx:%7.3f qy:%7.3f z:%7.3f    ", qdiff.w, qdiff.x, qdiff.y, qdiff.z);
	//printf("qw:%7.3f qx:%7.3f qy:%7.3f z:%7.3f    ", q.w, q.x, q.y, q.z);
	/*printf("kv0:%7.3f kv1:%7.3f   ", kvec_x.x, kvec_x.y);
	printf("kv0:%7.3f kv1:%7.3f   ", kvec_y.x, kvec_y.y);
	printf("kv0:%7.3f kv1:%7.3f   ", kvec_z.x, kvec_z.y);*/
	//printf("e0:%7.3f e1:%7.3f    ", E, e);
	/*printf("qw:%7.3f qx:%7.3f qy:%7.3f z:%7.3f    ", lq.w, lq.x, lq.y, lq.z);
	printf("y:%7.3f p:%7.3f r:%7.3f    ", y * RAD_TO_DEG, p * RAD_TO_DEG, r * RAD_TO_DEG);
	printf("alg:%d    ", coralg);
	
	//printf("w:%7.3f x:%7.3f y:%7.3f z:%7.3f   w:%7.3f x:%7.3f y:%7.3f z:%7.3f\n", qdiff.w, qdiff.x, qdiff.y, qdiff.z, q.w, q.x, q.y, q.z);
	//gxx::println(gyr[1], "\t", (qdiff * float4(50)));

	//printf("data update acc:(%7.3f,%7.3f,%7.3f) gyr:(%7.3f,%7.3f,%7.3f) mag:(%7.3f,%7.3f,%7.3f)\n", acc[0], acc[1], acc[2], gyr[0], gyr[1], gyr[2], mag[0], mag[1], mag[2]);
	//printf("acc:(%7.3f,%7.3f,%7.3f) gyr:(%7.3f,%7.3f,%7.3f) mag:(%7.3f,%7.3f,%7.3f) ahrs: q0:%7.3f q1:%7.3f q2:%7.3f q3:%7.3f y:%7.3f p:%7.3f r:%7.3f", acc[0], acc[1], acc[2], gyr[0], gyr[1], gyr[2], mag[0], mag[1], mag[2], q.w, q.x, q.y, q.z, y * RAD_TO_DEG + 180.0, p * RAD_TO_DEG, r * RAD_TO_DEG);
	printf("\n");*/
	//gxx::println(q, lq, );


	crow::release(pack);
}

#define MAXSIG 0.4

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
			crow::publish(thm, (const char*)data, sizeof(data));
			enabledata = false;
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}
}

int main() {
	//crow::enable_diagnostic();

	uint8_t _raddr[20];

	ahrs.reset();
	ahrs.setKoeff(50, 0.5);

	const char * raddr = ".12.192.168.1.135:10009"; 
	int rlen = hexer(_raddr, 20, raddr, strlen(raddr));

	crow_set_publish_host(_raddr, rlen);
	crow::subscribe("ahrs", 0, 200);

	//crow_udpgate udpgate;
	//udpgate.open(9999);

	crow_create_udpgate(9999, 12);

	crow_pubsub_handler = mhandler;

	//crow::link_gate(&udpgate, 12);

	auto thr = std::thread(publish_thread);
	thr.detach();

	crow_spin();
}
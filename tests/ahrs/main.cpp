#include <crow/pubsub.h>
#include <crow/gates/udpgate.h>

#include <gxx/print/stdprint.h>

#include <gxx/math/madgwick.h>
#include <gxx/math/linalg.h>
#include <gxx/print/linalg.h>

using namespace linalg::aliases;
using namespace linalg;

Madgwick ahrs;

float3 eg(0.0);

void mhandler(crow::packet* pack) {
	float4 lq;
	float4 q;
	float p;
	float r;
	float y;

	auto data = crow::pubsub_data(pack);

	//Размечаем данные в пакете.
	float3& acc = * (float3*) &data[0];
	float3& gyr = * (float3*) &data[12];
	float3& mag = * (float3*) &data[24];

	//Запоминаем текущее состояние.
	ahrs.readQuaternions(&lq.w,&lq.x,&lq.y,&lq.z);

	//Применяем новые данные.
	//ahrs.update(gyr[0], gyr[1], gyr[2], acc[0], acc[1], acc[2], mag[0], mag[1], mag[2]);
	//ahrs.update(gyr[0], gyr[1], gyr[2], acc[0], acc[1], acc[2]);
	ahrs.update(gyr[0], gyr[1], gyr[2]);
	
	//Запоминаем вычисленное состояние.
	ahrs.readQuaternions(&q.w,&q.x,&q.y,&q.z);



	//Вычисляем углы в интересующей нас системе координат.
	ahrs.getRotZYZ(&y, &p, &r);

	//auto qdiff = normalize( qmul(q, qinv(lq)) );

	auto qdiff = float4(1.0 / (1.0/(50))) * (q - lq);
    auto ww = float4(2) * qmul(qdiff, qinv(lq));
    auto w = qrot(qinv(lq), ww.xyz());

    eg = eg + (gyr - w - eg) * float3(0.0001);

    //gxx::println(w);

	//qdiff = qmul(qdiff, lq);

	/*float restorekoeff = 50 * 2;

	printf("x:%7.3f y:%7.3f z:%7.3f    ", qdiff.x * restorekoeff, qdiff.y * restorekoeff, qdiff.z * restorekoeff);
	//printf("x:%7.3f y:%7.3f z:%7.3f    ", qdiff.x, qdiff.y, qdiff.z);
	*/
	//printf("gx:%7.3f gy:%7.3f gz:%7.3f    ", gyr[0], gyr[1], gyr[2]);
	//printf("wx:%7.3f wy:%7.3f wz:%7.3f    ", w.x, w.y, w.z);
	//printf("egx:%7.3f egy:%7.3f egz:%7.3f    ", eg.x, eg.y, eg.z);
	//printf("qw:%7.3f qx:%7.3f qy:%7.3f z:%7.3f    ", qdiff.w, qdiff.x, qdiff.y, qdiff.z);
	printf("qw:%7.3f qx:%7.3f qy:%7.3f z:%7.3f    ", q.w, q.x, q.y, q.z);
	//printf("qw:%7.3f qx:%7.3f qy:%7.3f z:%7.3f    ", lq.w, lq.x, lq.y, lq.z);
	printf("y:%7.3f p:%7.3f r:%7.3f    ", y * RAD_TO_DEG, p * RAD_TO_DEG, r * RAD_TO_DEG);
	
	//printf("w:%7.3f x:%7.3f y:%7.3f z:%7.3f   w:%7.3f x:%7.3f y:%7.3f z:%7.3f\n", qdiff.w, qdiff.x, qdiff.y, qdiff.z, q.w, q.x, q.y, q.z);
	//gxx::println(gyr[1], "\t", (qdiff * float4(50)));

	//printf("data update acc:(%7.3f,%7.3f,%7.3f) gyr:(%7.3f,%7.3f,%7.3f) mag:(%7.3f,%7.3f,%7.3f)\n", acc[0], acc[1], acc[2], gyr[0], gyr[1], gyr[2], mag[0], mag[1], mag[2]);
	//printf("acc:(%7.3f,%7.3f,%7.3f) gyr:(%7.3f,%7.3f,%7.3f) mag:(%7.3f,%7.3f,%7.3f) ahrs: q0:%7.3f q1:%7.3f q2:%7.3f q3:%7.3f y:%7.3f p:%7.3f r:%7.3f", acc[0], acc[1], acc[2], gyr[0], gyr[1], gyr[2], mag[0], mag[1], mag[2], q.w, q.x, q.y, q.z, y * RAD_TO_DEG + 180.0, p * RAD_TO_DEG, r * RAD_TO_DEG);
	printf("\n");
	//gxx::println(q, lq, );


	crow::release(pack);
}

int main() {
	//crow::enable_diagnostic();

	ahrs.reset();
	ahrs.setKoeff(50, 0.5);

	crow::set_publish_host(".12.192.168.1.135:10009");
	crow::subscribe("ahrs", 4, crow::QoS(1));

	crow::udpgate udpgate;
	udpgate.open(9999);

	crow::pubsub_handler = mhandler;

	crow::link_gate(&udpgate, 12);

	crow::spin();
}
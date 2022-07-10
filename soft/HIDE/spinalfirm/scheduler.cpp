#include <genos/schedee.h>
#include <genos/ktimer.h>

void __schedule__()
{
	while (1)
	{
		crow::onestep();
		ktimer_manager_step();
		schedee_manager_step();
	}
}

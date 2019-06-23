package atom.mirmik.zippo_controller;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.Preference;
import android.preference.PreferenceActivity;
import android.preference.PreferenceFragment;
import android.support.v4.app.Fragment;

import java.util.Map;

public class Settings extends PreferenceActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        MyPreferenceFragment fragment = new MyPreferenceFragment();
        fragment.s = this;
        getFragmentManager().beginTransaction().replace(android.R.id.content, fragment).commit();

    }


    public static class MyPreferenceFragment extends PreferenceFragment implements SharedPreferences.OnSharedPreferenceChangeListener
    {
        Settings s;

        @Override
        public void onCreate(final Bundle savedInstanceState)
        {
            super.onCreate(savedInstanceState);
            addPreferencesFromResource(R.xml.preferences);

            SharedPreferences sharedPref = getPreferenceScreen().getSharedPreferences();
            sharedPref.registerOnSharedPreferenceChangeListener(this);

            findPreference("ip").setSummary(sharedPref.getString("ip", ""));
            findPreference("port").setSummary(sharedPref.getString("port", ""));

            //Map<String, ?> m = sharedPref.getAll();

            //for(Map.Entry<String, ?> entry : m.entrySet()) {
            //    String key = entry.getKey();
             //   String value = (String) entry.getValue();

             //   Preference pref = findPreference(key);
             //   pref.setSummary(value);
            //}
        }

        public void onSharedPreferenceChanged(SharedPreferences sharedPreferences, String key) {
            System.out.println("onSharedPreferenceChanged");
            System.out.println(key);

            Preference pref = findPreference(key);
            try {
                pref.setSummary(sharedPreferences.getString(key, ""));
            }
            catch (Throwable t)
            {
                //stuff
            }
        }
    }
}

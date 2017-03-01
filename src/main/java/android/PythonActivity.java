package android;

import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.widget.LinearLayout;
import android.widget.Button;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;


public class PythonActivity extends AppCompatActivity {
    static android.app.Activity instance;
    static org.python.Object _listener;

    /**
     * Set the object that will receive native application events
     *
     * Returns the activity instance.
     */
    static public android.app.Activity setListener(org.python.Object listener) {
        _listener = listener;
        return instance;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // There will only be one instance of this activity; store it.
        this.instance = this;
        Log.i("Python", "Starting Python app...");
        try {
            // Load the app module
            java.lang.Class app_module = java.lang.Class.forName("org.eliasdorneles.app.__init__");

            // Find the main method in the app module...
            java.lang.reflect.Method main = app_module.getMethod("main", java.lang.String[].class);

            // ... and invoke it.
            main.invoke(null, new java.lang.Object [] {
                new java.lang.String [] {"My Gradle App"}
            });

            if (_listener == null) {
                Log.w("Python", "My Gradle App didn't configure a listener.");
            } else {
                _listener.__setattr_null("_impl", new org.python.java.Object(this));
            }
            Log.d("Python", "Python app started.");
        } catch (java.lang.ClassNotFoundException e) {
            Log.e("Python", "Couldn't load Python app module.");
        } catch (java.lang.NoSuchMethodException e) {
            Log.e("Python", "Couldn't find main method.");
        } catch (java.lang.IllegalAccessException e) {
            Log.e("Python", "Couldn't access main method.");
        } catch (java.lang.reflect.InvocationTargetException e) {
            try {
                // e.getTargetException().printStackTrace();
                // If the Java method raised an Python exception, re-raise that
                // exception as-is. If it wasn"t a Python exception, wrap it
                // as one and continue.
                throw (org.python.exceptions.BaseException) e.getCause();
            } catch (ClassCastException java_e) {
                java.lang.String message = e.getCause().getMessage();
                if (message == null) {
                    message = e.getCause().getClass().getName();
                }
                throw new org.python.exceptions.RuntimeError(message);
            }
        }
        this.invoke_app_method("onCreate", null, null);
    }

    /**
     * Invoke an interface method on the Python
     */
    void invoke_app_method(
                java.lang.String method_name,
                org.python.Object [] args,
                java.util.Map<java.lang.String, org.python.Object> kwargs
            ) {
        Log.d("Python", "Invoking " + method_name + " method on Python listener.");
        if (_listener == null) {
            Log.e("Python", "Can't perform " + method_name +
                ": My Gradle App didn't configure a listener at creation.");
        } else {
            try {
                org.python.Object method = _listener.__getattribute_null(method_name);
                if (method != null) {
                    ((org.python.Callable) method).invoke(args, kwargs);
                } else {
                    Log.d("Python", "No " + method_name + " method on Python listener.");
                }
            } catch (java.lang.ClassCastException e) {
                Log.e("Python", method_name + " method isn't callable");
            }
        }
    }

    @Override
    public void onStart() {
        super.onStart();
        this.invoke_app_method("onStart", null, null);
    }

    @Override
    public void onResume() {
        super.onResume();
        this.invoke_app_method("onResume", null, null);
    }

    @Override
    public void onPause() {
        super.onPause();
        this.invoke_app_method("onPause", null, null);
    }

    @Override
    public void onStop() {
        super.onStop();
        this.invoke_app_method("onStop", null, null);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        this.invoke_app_method("onDestroy", null, null);
    }

    @Override
    public void onRestart() {
        super.onRestart();
        this.invoke_app_method("onRestart", null, null);
    }
}

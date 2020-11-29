package org.cnsl.ftms

import android.app.Application
import org.cnsl.ftms.di.allModules
import org.koin.android.ext.koin.androidContext
import org.koin.core.context.startKoin

class MainApplication : Application() {

    override fun onCreate() {
        super.onCreate()

        APPLICATION = this

        startKoin {
            androidContext(this@MainApplication)
            modules(allModules)
        }
    }

    companion object {
        private lateinit var APPLICATION: MainApplication

        fun getInstance(): MainApplication {
            return APPLICATION
        }
    }
}
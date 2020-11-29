package org.cnsl.ftms.repository.local.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import org.cnsl.ftms.R
import org.cnsl.ftms.repository.local.dao.ClientDao
import org.cnsl.ftms.repository.local.entities.Client

@Database(entities = arrayOf(Client::class), version = 1)
abstract class ClientDatabase : RoomDatabase() {

    abstract fun getClientDao(): ClientDao

    companion object {
        private var instance: ClientDatabase? = null

        fun getInstance(context: Context): ClientDatabase {
            return instance ?: synchronized(this) {
                instance ?: buildDatabase(context).also { instance = it }
            }
        }

        private fun buildDatabase(context: Context): ClientDatabase {
            return Room.databaseBuilder(
                context.applicationContext,
                ClientDatabase::class.java,
                context.getString(R.string.db_name)
            ).build()
        }
    }

}
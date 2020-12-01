package org.cnsl.ftms.repository.remote.database

import android.content.Context
import org.cnsl.ftms.R
import org.cnsl.ftms.repository.remote.dao.FileItemDao
import org.cnsl.ftms.repository.remote.dao.FileItemDaoImpl

class FileItemDatabase private constructor(private val host: String, private val port: Int) {

    fun getFileItemDao(): FileItemDao = FileItemDaoImpl(host, port)

    companion object {
        private var instance: FileItemDatabase? = null

        fun getInstance(context: Context): FileItemDatabase {
            return instance ?: synchronized(this) {
                instance ?: buildDatabase(context).also { instance = it }
            }
        }

        private fun buildDatabase(context: Context): FileItemDatabase {
            return FileItemDatabase(
                context.getString(R.string.server_host),
                Integer.valueOf(context.getString(R.string.server_port))
            )
        }
    }
}
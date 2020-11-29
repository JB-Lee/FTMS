package org.cnsl.ftms.repository.local.dao

import androidx.room.*
import org.cnsl.ftms.repository.local.entities.Client

@Dao
interface ClientDao {

    @Query("SELECT * FROM client")
    fun getAll(): List<Client>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insert(vararg item: Client)

    @Delete
    fun delete(vararg item: Client)

    @Query("DELETE FROM client")
    fun deleteAll()
}
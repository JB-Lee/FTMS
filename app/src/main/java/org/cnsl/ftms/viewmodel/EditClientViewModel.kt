package org.cnsl.ftms.viewmodel

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.view.View
import androidx.lifecycle.LifecycleObserver
import androidx.lifecycle.ViewModel
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.utils.CustomMutableLiveData
import org.cnsl.ftms.view.EditClientActivity
import org.cnsl.ftms.view.ManageActivity

class EditClientViewModel(val context: Context, val _client: Client) : ViewModel(), LifecycleObserver {
    val client: CustomMutableLiveData<Client> by lazy { CustomMutableLiveData(_client) }

    fun onRegisterClick(view: View) {
        val intent = Intent(view.context, ManageActivity::class.java).apply {
            putExtra("client", client.value)
        }

        (view.context as EditClientActivity).apply {
            setResult(Activity.RESULT_OK, intent)
            finish()
        }
    }


}
package org.cnsl.ftms.viewmodel

import android.content.Context
import android.content.Intent
import android.view.View
import androidx.lifecycle.*
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.cnsl.ftms.repository.local.database.ClientDatabase
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.repository.remote.database.FileItemDatabase
import org.cnsl.ftms.utils.LiveArrayList
import org.cnsl.ftms.view.EditClientActivity
import org.cnsl.ftms.view.ManageActivity
import org.cnsl.ftms.view.RegisterClientActivity
import org.cnsl.ftms.view.TransferActivity

class ManageViewModel(val context: Context, val clientView: RecyclerView) : ViewModel(), LifecycleObserver {
    val clients = LiveArrayList<Client>()
    val selectClients = LiveArrayList<Client>()

    var onEdit: Client? = null

    fun checkConnection() {
        viewModelScope.launch(Dispatchers.IO) {
            FileItemDatabase.getInstance(context).getFileItemDao().apply {
                clients.forEach {
                    val available = ping(it.id)
                    withContext(Dispatchers.Main) {
                        it.isAvailable.value = available
                    }
                }
            }
            withContext(Dispatchers.Main) {
                clientView.adapter?.notifyDataSetChanged()
            }
        }
    }

    fun onClientRefresh(srl: SwipeRefreshLayout) {
        checkConnection()
        srl.isRefreshing = false
    }

    @OnLifecycleEvent(Lifecycle.Event.ON_CREATE)
    fun onInit() {
        viewModelScope.launch(Dispatchers.IO) {
            val list = ClientDatabase.getInstance(context).getClientDao().getAll()
            withContext(Dispatchers.Main) {
                clients.clear(false)
                clients.addAll(list)
            }
            checkConnection()
        }
    }

    @OnLifecycleEvent(Lifecycle.Event.ON_DESTROY)
    fun onDestroy() {
        viewModelScope.launch(Dispatchers.IO) {
            clients.value?.let {
                ClientDatabase.getInstance(context)
                    .getClientDao().apply {
                        deleteAll()
                        insert(*it.toTypedArray())
                    }
            }
        }

    }

    fun onMainFabClick(view: View) {
        (view.context as ManageActivity).apply {
            toggleFab()
        }
    }

    fun onAddClientFabClick(view: View) {
        val intent = Intent(view.context, RegisterClientActivity::class.java)
        (view.context as ManageActivity).apply {
            startActivityForResult(intent, 1)
        }
    }

    fun onTransferFabClick(view: View) {
        if (selectClients.size != 2) return

        val intent = Intent(view.context, TransferActivity::class.java)
        intent.apply {
            putExtra("client a", selectClients[0])
            putExtra("client b", selectClients[1])
        }
        (view.context as ManageActivity).apply {
            startActivityForResult(intent, 3)
        }
    }

    fun onEditClientClick(view: View, client: Client) {
        val intent = Intent(view.context, EditClientActivity::class.java)
        intent.putExtra("client", client)
        onEdit = client
        (view.context as ManageActivity).apply {
            startActivityForResult(intent, 2)
        }
        clients.remove(client)
    }


}
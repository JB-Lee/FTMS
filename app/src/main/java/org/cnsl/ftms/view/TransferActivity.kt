package org.cnsl.ftms.view

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import kotlinx.android.synthetic.main.activity_manage.*
import org.cnsl.ftms.R
import org.cnsl.ftms.adapter.FileItemAdapter
import org.cnsl.ftms.databinding.ActivityTransferBinding
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.viewmodel.TransferViewModel
import org.koin.androidx.viewmodel.ext.android.viewModel
import org.koin.core.parameter.parametersOf

class TransferActivity : AppCompatActivity() {

    val viewModel: TransferViewModel by viewModel {
        parametersOf(
            intent.getParcelableExtra<Client>("client a"),
            intent.getParcelableExtra<Client>("client b")
        )
    }
    val binding: ActivityTransferBinding by lazy { DataBindingUtil.setContentView(this, R.layout.activity_transfer) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)


        binding.apply {
            vm = viewModel
            lifecycleOwner = this@TransferActivity
        }


        binding.recyclerView1.apply {
            adapter = FileItemAdapter(viewModel)
            layoutManager = LinearLayoutManager(super.getBaseContext())
            addItemDecoration(DividerItemDecoration(this@TransferActivity, LinearLayoutManager.VERTICAL))
        }

        binding.recyclerView2.apply {
            adapter = FileItemAdapter(viewModel)
            layoutManager = LinearLayoutManager(super.getBaseContext())
            addItemDecoration(DividerItemDecoration(this@TransferActivity, LinearLayoutManager.VERTICAL))
        }

        lifecycle.addObserver(viewModel)
    }
}
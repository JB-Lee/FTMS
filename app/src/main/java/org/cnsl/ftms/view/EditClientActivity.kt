package org.cnsl.ftms.view

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import org.cnsl.ftms.R
import org.cnsl.ftms.databinding.ActivityEditClientBinding
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.viewmodel.EditClientViewModel
import org.koin.androidx.viewmodel.ext.android.viewModel
import org.koin.core.parameter.parametersOf

class EditClientActivity : AppCompatActivity() {

    val viewModel: EditClientViewModel by viewModel { parametersOf(intent.getParcelableExtra<Client>("client")) }

    val binding: ActivityEditClientBinding by lazy {
        DataBindingUtil.setContentView(
            this,
            R.layout.activity_edit_client
        )
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding.apply {
            vm = viewModel
            lifecycleOwner = this@EditClientActivity
        }

        lifecycle.addObserver(viewModel)

    }


}
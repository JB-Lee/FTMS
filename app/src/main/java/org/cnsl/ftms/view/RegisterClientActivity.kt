package org.cnsl.ftms.view

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import org.cnsl.ftms.R
import org.cnsl.ftms.databinding.ActivityRegisterClientBinding
import org.cnsl.ftms.viewmodel.RegisterClientViewModel
import org.koin.android.ext.android.inject

class RegisterClientActivity : AppCompatActivity() {

    val viewModel: RegisterClientViewModel by inject()
    val binding: ActivityRegisterClientBinding by lazy {
        DataBindingUtil.setContentView(
            this,
            R.layout.activity_register_client
        )
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding.apply {
            vm = viewModel
            lifecycleOwner = this@RegisterClientActivity
        }

        lifecycle.addObserver(viewModel)
    }
}
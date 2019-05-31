import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  LoginForm: FormGroup = new FormGroup({
    username : new FormControl(''),
    password : new FormControl(''),
  });

  constructor(private API: apiServices) { }

  ngOnInit() {
    
  }

  onSubmit(){
    this.API.loginAPI(this.LoginForm.value.username, this.LoginForm.value.password).subscribe(
      (response)=>{
        console.log(response);  
      }
    )
    

  }

}

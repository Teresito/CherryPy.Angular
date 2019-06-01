import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { apiServices } from '../services/apiServices';
import { AuthGuard } from '../services/auth-guard.service';
import { componentState } from '../services/componentService';


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

  constructor(private API: apiServices, private auth: AuthGuard, private state: componentState, private router: Router) { }

  wrongCreds: boolean = false;

  ngOnInit() {

  }

  onSubmit(){
    this.wrongCreds = false;
    this.API.loginAPI(this.LoginForm.value.username, this.LoginForm.value.password).subscribe(
      (response)=>{
        console.log(response);  
        if(response === "0"){
          this.wrongCreds = true;
        }
        else if(response === "1"){
          this.wrongCreds = false;
          this.state.loggedIn = true;
          this.state.loggedChanged.next();
          this.router.navigate(['/broadcast']);
        }
      }
    )
    

  }

}

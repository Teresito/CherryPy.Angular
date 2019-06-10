import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { apiServices } from '../services/apiServices';
import { AuthGuard } from '../services/auth-guard.service';
import { componentState } from '../services/componentService';
import { webServer } from '../constants'


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  LoginForm: FormGroup = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
  });

  constructor(private API: apiServices, private state: componentState, private router: Router) { }
  
  wrongLogin: boolean = false;
  loading: boolean = false;
  badAccessMessage: boolean = false;
  badServer: boolean = false;

  // Initialize the component with these parameters and function calls
  ngOnInit() {
    if(sessionStorage.getItem('authenticated')){
      this.router.navigate(['/broadcast'])
    }
    if (Boolean(sessionStorage.getItem('badAccess'))){
      this.badAccessMessage = Boolean(sessionStorage.getItem('badAccess'));
      setTimeout(() => {
        sessionStorage.removeItem('badAccess')
        this.badAccessMessage = false;
      }, 3000);
    }

  }
  // Submits the user information to backend
  onSubmit() {
    this.loading = true;
    this.wrongLogin = false;
    let username = this.LoginForm.value.username;
    let password = this.LoginForm.value.password;
    this.API.loginAPI(username, password).then(
      (response) => {
        
        this.wrongLogin = false
        if (response == '1') {
          this.state.setClient(username, true)
        }
        else if (response == 'error'){
          this.badServer = true;
        }
        else {
          this.wrongLogin = true;
        }
        this.loading = false;
      }
    );
  }

}

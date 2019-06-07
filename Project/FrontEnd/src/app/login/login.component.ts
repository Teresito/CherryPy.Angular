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

  constructor(private API: apiServices, private state: componentState, private router: Router) { }

  wrongCreds: boolean = false;

  ngOnInit() {
    //console.log(this.state.getLoggedIn())
    if(this.state.getLoggedIn()==true){
      this.router.navigate(['/broadcast']);
    }
    this.state.setNotify(true)
    this.API.loginAPI('tmag741', 'Teresito_419588351').subscribe(
      (response)=>{
        console.log(response);  
        if(response === "0"){
          this.wrongCreds = true;
        }
        else if(response === "1"){
          this.wrongCreds = false;
          this.state.setLoggedIn(true);
          this.state.loggedChanged.next();
          this.API.reportUser();
          this.router.navigate(['/broadcast']);
        }
      }
    )
  }

  onSubmit(){
    this.wrongCreds = false;
    this.API.loginAPI(this.LoginForm.value.username, this.LoginForm.value.password).subscribe(
      (response)=>{
        if(response === "0"){
          this.wrongCreds = true;
        }
        else if(response === "1"){
          this.wrongCreds = false;
          this.state.setLoggedIn(true);
          this.state.loggedChanged.next();
          this.API.reportUser();
          this.router.navigate(['/broadcast']);
        }
      }
    )
    

  }

}

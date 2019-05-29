import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { flattenStyles } from '@angular/platform-browser/src/dom/dom_renderer';
import { conditionallyCreateMapObjectLiteral } from '@angular/compiler/src/render3/view/util';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  private user: string = "a";
  private pass: string = "a";
  private fakePage: boolean = false;

  LoginForm: FormGroup = new FormGroup({
    username : new FormControl(''),
    password : new FormControl(''),
  });

  constructor() { }

  ngOnInit() {
    
  }

  onSubmit(){
    if(this.LoginForm.value.username === this.user && this.LoginForm.value.password === this.pass){
      this.fakePage = true;
      console.log("WAT");
    }
  }

}

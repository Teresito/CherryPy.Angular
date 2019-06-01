import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { FormGroup, FormControl } from '@angular/forms';
import { componentState } from '../services/componentService';
import { AuthGuard } from '../services/auth-guard.service';
@Component({
  selector: 'app-privatedata',
  templateUrl: './privatedata.component.html',
  styleUrls: ['./privatedata.component.css']
})
export class PrivatedataComponent implements OnInit {

  eKeyForm: FormGroup = new FormGroup({
    newEKey: new FormControl(''),
    EKeyAgain: new FormControl(''),
    Dkey: new FormControl(''),
  });

  decryptForm: boolean = false;
  encryptForm: boolean = false;
  options: boolean = false;
  optionsBack: boolean = false;

  constructor(private API: apiServices, private state: componentState) { }

  wrongKey: boolean = false;
  pholder = "Encryption Key";
  buttonKey: String;
  dataReponse: String;

  ngOnInit() {
    if (this.state.eKeyNotify === true) {
      this.API.checkPrivateData().subscribe(
        (response) => {
          if (response == "ok") {
            this.options = true;
            this.optionsBack = true;
            this.buttonKey = "Decrypt";
            this.dataReponse = "It seems like you have private data in the login server";
          }
          else if (response == "error") {
            this.encryptForm = true;
            this.buttonKey = "Encrypt";
            this.dataReponse = "It seems like you don't have any private data in the login server. To proceed enter your key for encryption";
          }
        }
      );

      this.state.eKeyNotify = false;
    }

  }

  NewKey(){
    this.encryptForm = true;
    this.buttonKey = "Encrypt";
    this.options = false;
  }

  Back(){
    this.options = true;
    this.encryptForm = false;
    this.decryptForm = false;
    this.state.loggedChanged.next();
  }

  DecryptKey(){
    this.decryptForm = true;
    this.buttonKey = "Decrypt";
    this.options = false;
  }


  encryptSubmit(){
    this.wrongKey = false;
    if (this.eKeyForm.value.newEKey == this.eKeyForm.value.EKeyAgain){
      this.API.newPrivateData().subscribe(
        (response)=>{
          if(response === "ok"){
            this.state.loggedChanged.next();
          }
          else{
            console.log("ERROR WITH SERVER")
          }
        }
      );
    }
    else{
      this.wrongKey = true;
    }

  }

  decryptSubmit(){

  }

}
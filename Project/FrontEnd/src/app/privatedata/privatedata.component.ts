import { Component, OnInit } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { FormGroup, FormControl } from '@angular/forms';
import { componentState } from '../services/componentService';

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
  dataResponse: String;

  ngOnInit() {
    if (this.state.eKeyNotify === true) {
      this.API.checkPrivateData().subscribe(
        (response) => {
          if (response == "1") {
            this.options = true;
            this.optionsBack = true;
            this.buttonKey = "Decrypt";
            this.dataResponse = "It seems like you have private data in the login server";
          }
          else if (response == "0") {
            this.encryptForm = true;
            this.buttonKey = "Encrypt";
            this.dataResponse = "It seems like you don't have any private data in the login server. To proceed enter your key for encryption";
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
    this.dataResponse = "Enter your new key. Minimum 5 characters"
  }

  Back(){
    this.options = true;
    this.encryptForm = false;
    this.decryptForm = false;
    this.dataResponse = "What is your choice?"
  }

  DecryptKey(){
    this.decryptForm = true;
    this.buttonKey = "Decrypt";
    this.options = false;
    this.dataResponse = "Let's decrypt it !"
  }


  encryptSubmit(){
    this.wrongKey = false;
    let uniqueKey = this.eKeyForm.value.newEKey;
    this.API.newPrivateData(uniqueKey).subscribe(
      (response) => {
        if (response === "1") {
          this.state.loggedChanged.next();
        }
        else {
          this.wrongKey = true;
        }
      }
    );

  }

  decryptSubmit(){
    let uniqueKey = this.eKeyForm.value.Dkey;
    this.API.unlockData(uniqueKey).subscribe(
      (response) => {
        if (response === "1") {
          this.state.loggedChanged.next();
        }
        else {
          this.wrongKey = true;
        }
      }
    );
  }

}

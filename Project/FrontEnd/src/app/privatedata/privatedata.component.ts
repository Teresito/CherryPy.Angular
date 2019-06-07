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
  loading: boolean = true;

  constructor(private API: apiServices, private state: componentState) { }

  wrongKey: boolean = false;
  pholder = "Encryption Key";
  buttonKey: String;
  dataResponse: String;

  ngOnInit() {
    this.API.checkPrivateData().then(
      (response) => {
        if (response == "1") {
          this.options = true;
          this.optionsBack = true;
          this.buttonKey = "Decrypt";
          this.dataResponse = "It seems like you have private data in the login server";
          this.loading = false;
        }
        else if (response == "0") {
          this.encryptForm = true;
          this.buttonKey = "Encrypt";
          this.dataResponse = "To proceed, enter your key for encryption. Minimum 5 characters";
          this.loading = false;
        }
      }
    );


  }

  NewKey() {
    this.encryptForm = true;
    this.buttonKey = "Encrypt";
    this.options = false;
    this.dataResponse = "Note: You will not see your past messages. Enter your new key. Minimum 5 characters. "
  }

  Back() {
    this.options = true;
    this.wrongKey = false;
    this.encryptForm = false;
    this.decryptForm = false;
    this.dataResponse = "What is your choice?"
  }

  DecryptKey() {
    this.decryptForm = true;
    this.buttonKey = "Decrypt";
    this.options = false;
    this.dataResponse = "Let's decrypt it !"
  }


  encryptSubmit() {
    this.wrongKey = false;
    this.loading = true;
    let uniqueKey = this.eKeyForm.value.newEKey;
    let match = this.eKeyForm.value.EKeyAgain;
    if(match == uniqueKey){
      this.API.newPrivateData(uniqueKey).then((response) => {
        if (response == '1') {
          sessionStorage.setItem('inSession', true.toString())
          this.state.session.next();
        }
        else {
          this.wrongKey = true;
          this.loading = false;
        }
      });
    }
    else{
      this.wrongKey = true;
      this.loading = false;
    }

  }

  decryptSubmit() {
    this.wrongKey = false;
    this.loading = true;

    let uniqueKey = this.eKeyForm.value.Dkey;
    this.API.unlockData(uniqueKey).then((response) => {
      if (response == '1') {
        sessionStorage.setItem('inSession', true.toString())
        this.state.session.next();
      }
      else if (response == 0) {
        this.wrongKey = true;
        this.loading = false;
      }
    });
  }

}

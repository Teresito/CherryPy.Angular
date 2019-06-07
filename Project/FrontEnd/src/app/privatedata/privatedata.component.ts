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
    this.loading = true;
    if (this.state.getNotify() === true) {
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
            this.dataResponse = "To proceed, enter your key for encryption. Minimum 5 characters";
          }
          else if(response == '2'){
            this.state.logout();
          }
          this.loading = false;
        }
      );
      
      // this.API.unlockData('asd123').subscribe(
      //   (response) => {
      //     if (response === "1") {
      //       this.state.startSession(true);
      //       this.state.session.next();
      //       this.API.reportUser();
      //     }
      //     else {
      //       this.wrongKey = true;
      //     }
      //     this.loading = false;
      //   }
      // );


    }


  }

  NewKey(){
    this.encryptForm = true;
    this.buttonKey = "Encrypt";
    this.options = false;
    this.dataResponse = "Note: You will not see your past messages. Enter your new key. Minimum 5 characters. "
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
    this.loading = true;
    this.API.newPrivateData(uniqueKey).subscribe(
      (response) => {
        if (response === "1") {
          this.state.startSession(true);
          this.state.session.next();
          this.API.reportUser();
        }
        else {
          this.wrongKey = true;
        }
        this.loading = false;
      }
    );
  }

  decryptSubmit(){
    let uniqueKey = this.eKeyForm.value.Dkey;
    this.loading = true;
    this.API.unlockData(uniqueKey).subscribe(
      (response) => {
        if (response === "1") {
          this.state.startSession(true);
          this.state.session.next();
          this.API.reportUser();
        }
        else {
          this.wrongKey = true;
        }
        this.loading = false;
      }
    );
  }

}

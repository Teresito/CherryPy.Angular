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

  constructor(private API: apiServices, private state: componentState) { }

  wrongKey: boolean = false;
  pholder = "Encrpytion Key";
  buttonKey: String;
  dataReponse: String;
  ngOnInit() {
    if (this.state.eKeyNotify === true) {
      this.API.checkPrivateData().subscribe(
        (response) => {
          if (response == "ok") {
            this.decryptForm = true;
            this.buttonKey = "Decrypt";
            this.dataReponse = "It seems like you have private data in the login server";
          }
          else if (response == "error") {
            this.encryptForm = true;
            this.buttonKey = "Encrypt";
            this.dataReponse = "It seems like you don't have any private data in the login server";
          }
        }
      );
      this.state.eKeyNotify = false;
    }

  }

  decryptSubmit() {
    this.wrongKey = true;
  }

  encryptSubmit() {

  }
}

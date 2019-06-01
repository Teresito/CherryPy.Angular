import { Component, OnInit, DoCheck } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { FormGroup, FormControl } from '@angular/forms';
import { componentState } from '../services/componentService';
import { AuthGuard } from '../services/auth-guard.service';
@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit {
  
  Dkey: FormControl = new FormControl('');

  eKeyForm: FormGroup = new FormGroup({
    newEKey: new FormControl(''),
    EKeyAgain: new FormControl(''),
  });
  
  dKeyForm: FormGroup = new FormGroup({
    Dkey: new FormControl(''),
  });



  constructor(private API: apiServices, private state: componentState, private auth: AuthGuard) { }

  toggleDecrypt: String = 'none';
  toggleEncrypt: String = 'none';
  wrongKey: boolean = false;
  pholder = "Encrpytion Key";

  ngOnInit() {
    if (this.state.eKeyNotify === true) {     
      this.API.checkPrivateData().subscribe(
        (response) => {
          if (response == "ok") {
            this.toggleDecrypt = 'block';
          }
          else if (response == "error"){
            this.toggleEncrypt = 'block';
          }
        }
      );
      this.state.eKeyNotify = false;
    }
    else {
      this.toggleDecrypt = 'none';
    }


  }

  decryptSubmit() {
    this.wrongKey = true;
  }

}

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

  eKeyForm: FormGroup = new FormGroup({
    key: new FormControl(''),
  });

  constructor(private API: apiServices, private state: componentState, private auth: AuthGuard) { }

  toggleModal: String;
  wrongKey: boolean = false;
  pholder = "Encrpytion Key";

  ngOnInit() {
    if (this.state.eKeyNotify === true){
      this.toggleModal = 'block';
      this.state.eKeyNotify = false;
    }
    else{
      this.toggleModal = 'none';
    }
    // TESTING
    // this.API.endpointAPI().subscribe(
    //   (response) => {
    //     console.log(response);
    //   }
    // )
  }

  onSubmit(){
    console.log(this.eKeyForm.value.key);
    this.wrongKey = true;
  }

}

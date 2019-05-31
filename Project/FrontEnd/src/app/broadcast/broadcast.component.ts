import { Component, OnInit, DoCheck } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { FormGroup, FormControl } from '@angular/forms';
import { componentState } from '../services/componentService';
@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit {

  eKeyForm: FormGroup = new FormGroup({
    key: new FormControl(''),
  });

  constructor(private API: apiServices, private state: componentState) { }

  toggleModal: String;
  wrongKey: boolean = true;
  pholder = "Encrpytion Key";

  ngOnInit() {
    if (this.state.eKeyNotify === true){
      this.toggleModal = 'block';
      this.state.eKeyNotify = false;
    }
    else{
      this.toggleModal = 'none';
    }

    this.API.endpointAPI().subscribe(
      (response) => {
        console.log(response);
      }
    )
  }

}

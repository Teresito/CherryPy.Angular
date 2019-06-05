import { Component, OnInit, DoCheck } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';

@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit {
  
  toggleModal: String = "block";

  constructor(private API: apiServices, private state: componentState,){

  }

  ngOnInit(){
    if (this.state.eKeyNotify) {
      this.toggleModal = 'block';
    }
    else{
      this.toggleModal = 'none';
    }
    this.state.session.subscribe(
      ()=>{
        if(this.state.inSession){
          this.toggleModal = 'none';
        }
      }
    );

  }

}

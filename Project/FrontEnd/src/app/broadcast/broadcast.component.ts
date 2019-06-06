import { Component, OnInit, DoCheck } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit {
  
  toggleModal: String = "block";
  message = new FormControl('');
  loading: boolean = false;
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
          this.state.loggedChanged.next()
          this.toggleModal = 'none';
        }
      }
    );
      
  }

  sendMessage(){
    console.log("wat")
    this.API.broadcast(this.message.value).subscribe(
      (response)=>{
        this.loading = true;
        if (response == '1'){
          setTimeout(() => {
            this.loading = false;
          }, 3000);
          this.message.patchValue(null)
        }
      }
    );
  }

}

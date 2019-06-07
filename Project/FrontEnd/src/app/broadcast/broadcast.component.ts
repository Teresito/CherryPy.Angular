import { Component, OnInit, DoCheck } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';
import { FormControl } from '@angular/forms';
import { CommonModule, DatePipe  } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit {
  
  toggleModal: String = "block";
  message = new FormControl('');
  loading: boolean = false;
  messageList: any;
  testDate = Date.now();
  
  constructor(private API: apiServices, private state: componentState, private router: Router){

  }

  ngOnInit(){
    this.fetchPublicMessages();
    if (this.state.getNotify()) {
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
    this.API.broadcast(this.message.value).subscribe(
      (response)=>{
        this.fetchPublicMessages();
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

  fetchPublicMessages(){    
    this.API.get_broadcastMessages().subscribe(
      (response)=>{
        this.messageList = response['public_messages']
      }
    );
  }

}

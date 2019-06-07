import { Component, OnInit, DoCheck } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';
import { FormControl } from '@angular/forms';
import { CommonModule, DatePipe } from '@angular/common';
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
  messageLoading: boolean = true;
  messageList: any;
  testDate = Date.now();

  constructor(private API: apiServices, private state: componentState, private route: Router) {

  }

  ngOnInit() {
    this.messageList = this.API.get_broadcastMessages().then(
      (response) => {
        this.messageList = response;
        this.messageLoading = false;
      }
    );
    if (this.state.notified) {
      this.toggleModal = 'block'
    }
    else {
      this.toggleModal = 'none'
    }
  }

  sendMessage() {

  }

  fetchPublicMessages() {

  }

}

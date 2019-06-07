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
  notify: boolean;
  testDate = Date.now();

  constructor(private API: apiServices, private state: componentState, private route: Router) {

  }

  ngOnInit() {
    this.fetchPublicMessages();
    this.state.session.subscribe(
      () => {
        if (Boolean(sessionStorage.getItem('inSession'))) {
          this.toggleModal = 'none';
        }
      });

    this.notify = !Boolean(sessionStorage.getItem('inSession'));

  }

  sendMessage() {
    this.API.broadcast(this.message.value);
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
      this.message.patchValue(null);
      this.fetchPublicMessages();
    }, 2000);
  }

  fetchPublicMessages() {
    this.messageLoading = true;
    this.messageList = this.API.get_broadcastMessages().then(
      (response) => {
        this.messageList = response;
        this.messageLoading = false;
      }
    );
  }

}

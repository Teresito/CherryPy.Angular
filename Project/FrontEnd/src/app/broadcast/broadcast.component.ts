import { Component, OnInit, DoCheck, HostListener } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';
import { FormControl } from '@angular/forms';
import { CommonModule, DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { MarkdownService } from 'ngx-markdown';
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

  blockLoading = false;
  favLoading = false;

  isSearching = false;
  searchList = [];
  searchZero = false;
  searched: string;

  showMarked = false;
  modalMarked = 'none';
  markedDownMessage: string;
  broadTimer: any;


  constructor(private API: apiServices, private state: componentState, private markService: MarkdownService) {

  }

  ngOnInit() {
    this.fetchPublicMessages();
    this.state.session.subscribe(
      () => {
        if (Boolean(sessionStorage.getItem('inSession'))) {
          this.toggleModal = 'none';
        }

        if (Boolean(sessionStorage.getItem('inSession')))
          this.broadTimer = setInterval(() => {
            this.fetchPublicMessages();
          }, 30000)
        else {
          clearInterval(this.broadTimer);
        }
      });


    this.state.searchTrigger.subscribe((search) => {
      if (search != '' || search != null) {
        this.searchList = [];
        this.isSearching = true;
        this.searchZero = false;
        for (let index = 0; index < this.messageList.length; index++) {
          // this.searchList = this.messageList[index][0];
          if (this.messageList[index][0].substring(0, search.length) == search) {
            this.searchList.push(this.messageList[index]);
          }
        }
        if (this.searchList.length == 0) {
          this.searchZero = true;
          this.searched = search;
        }
      }
      else {
        this.searchList = [];
        this.searchZero = false;
        this.isSearching = false;
      }
    });
    this.notify = !Boolean(sessionStorage.getItem('inSession'));

  }

  showMarkDown(message: string) {
    this.showMarked = true;
    this.modalMarked = 'block';

    // this.markedDownMessage = this.markService.compile(message);
    this.markedDownMessage = message
    // console.log(message)
    // console.log(this.markedDownMessage)


  }

  closeMarkDown() {
    this.showMarked = false;
    this.modalMarked = 'none';
    this.markedDownMessage = null;
  }

  onKeydown(event) {
    if (!this.loading) {
      this.sendMessage();
    }
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

  backToTop(){
    window.scrollTo(0, 0);
  }

  updateList(){
    this.messageLoading = true;
    setTimeout(() => {
      this.fetchPublicMessages();
    }, 2000);

  }

  fetchPublicMessages() {
    this.messageLoading = true;
    this.API.get_broadcastMessages().then(
      (response) => {
        console.log(response.length + " From DB")

        for (let index = 0; index < response.length; index++) {
          response[index][2] = response[index][2] * 1000;
          if (response[index][1].includes('!Meta') && (response[index][1].match(/:/g) || []).length == 2) {
            let meta_messages = response[index][1].split(":", 3)
            meta_messages[2] = meta_messages[2].replace("[", "").replace("]", "")
            // ITERATE AND MODIFY 
            if (meta_messages[1] == 'favourite_broadcast' || meta_messages[1] == 'block_broadcast') {
              for (let j = 0; j < response.length; j++) {

                if (response[j][4] == meta_messages[2]) { // SIGNATURE MATCH
                  if (meta_messages[1] == 'favourite_broadcast') {
                    if (sessionStorage.getItem('username') == response[index][0]) {
                      response[j][1] = response[j][1] + " | You 💖 this";
                    }
                    else {
                      response[j][1] = response[j][1] + " | " + response[index][0] + " 💖 this";
                    }
                  }
                  else if (meta_messages[1] == 'block_broadcast') {
                    if (sessionStorage.getItem('username') == response[index][0]) {
                      response[j][1] = "⛔You have blocked this message⛔";
                    }
                    else {
                      response[j][1] = response[j][1] + " | " + response[index][0] + " ⛔ this";
                    }
                  }
                }

              }
            }

          }

        }

        for (let index = 0; index < response.length; index++) {
          if (response[index][1].includes('!Meta') || response[index][1].indexOf('!Meta') > -1) {
            response.splice(index, 1)
            index = 0;
          }
        }
        for (let index = 0; index < response.length; index++) {
          if (response[index][1].includes('!Meta') || response[index][1].indexOf('!Meta') > -1) {
            response.splice(index, 1)
            index = 0;
          }
        }
        
        console.log(response.length + " Removed !META")
        this.messageList = response;
        this.messageLoading = false;
      }
    );
  }

  favouriteMessage(messageIndex: number){
    this.favLoading = true;
    this.API.broadcast("!Meta:favourite_broadcast:[" + this.messageList[messageIndex][4] + "]")
    setTimeout(() => {
      this.favLoading = false;
      this.fetchPublicMessages();
    }, 2500);
  }

  blockMessage(messageIndex: number){
    this.blockLoading = true;

    this.API.broadcast("!Meta:block_broadcast:[" + this.messageList[messageIndex][4] + "]");
    setTimeout(() => {
      this.blockLoading = false;
      this.fetchPublicMessages();
    }, 2500);
  }


}

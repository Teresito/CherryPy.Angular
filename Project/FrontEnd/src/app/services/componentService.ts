import { Subject } from 'rxjs';
import { Injectable } from '@angular/core';
import { apiServices } from './apiServices';
import { Router } from '@angular/router';

@Injectable()
export class componentState {

    constructor(private API: apiServices){}

    eKeyNotify = true;
    inSession = false;
    
    session = new Subject<any>();
    loggedChanged = new Subject<any>();
    usersUpdated = new Subject<any>();

    reportTimer: any;
    usersTimer: any;
    onlineUsers: any;

    setLoggedIn(bool: boolean){
        sessionStorage.setItem('loggedIn', String(bool));
    }

    getLoggedIn(){
        return Boolean(sessionStorage.getItem('loggedIn'));
    }

    deleteSession(){
        sessionStorage.clear();
    }

    startSession(session:boolean){
        this.inSession = session;
        if(session){
            // Call once
            this.reportUser();
            this.updateUsers();
            // Call intervally
            this.reportTimer = setInterval( ()=>{this.reportUser()}, 10000); // 10 Seconds
            this.usersTimer = setInterval(() => { this.updateUsers()}, 60000); // 1 minute
        }
        else{
            clearInterval(this.reportTimer);
        }
    }


    private reportUser(){
        this.API.reportUser().subscribe((response) => {
            if (response == '0') {
                this.setLoggedIn(false);
                this.loggedChanged.next();
                this.session.next();
                clearInterval(this.reportTimer);
            }
        })
    }

    private updateUsers(){
        this.API.listUserAPI().subscribe((response) => {
            this.onlineUsers = response['userList'];
            this.usersUpdated.next();
             if (response == '0') {
                this.setLoggedIn(false);
                this.loggedChanged.next();
                this.session.next();
                clearInterval(this.usersTimer);
            }
        })
    }
}
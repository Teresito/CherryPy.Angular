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
    reportTimer: any;

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
            this.reportTimer = setInterval(() =>
                this.API.reportUser().subscribe((response) => {
                    console.log(response)
                    if (response == '0') {
                        this.setLoggedIn(false);                       
                        this.loggedChanged.next();
                        this.session.next();
                        clearInterval(this.reportTimer);
                    }
                })
                , 5000);
        }
        else{
            clearInterval(this.reportTimer);
        }
    }

}
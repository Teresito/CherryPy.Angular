import { HttpClient, HttpHeaders } from '@angular/common/http';
import { webServer } from '../constants';
import { Injectable } from '@angular/core';


@Injectable()
export class apiServices {

    constructor(private httpClient: HttpClient) { }

    public listUserAPI() {
        return this.httpClient.post(`${webServer}/onlineUsers`, null, { responseType: 'json' });
    }    

    public pingAPI() {
        return this.httpClient.post(`${webServer}/ping`, null, { responseType: 'text' });
    }

    public loginAPI(user: String, pass: String) {
        return this.httpClient.post(`${webServer}/login`, {"user":user, "pass":pass}, { responseType: 'text' });
    }

    public logoutAPI(){
        return this.httpClient.post(`${webServer}/logout`, null, { responseType: 'text' });
    }
    
    public checkPrivateData(){
        return this.httpClient.post(`${webServer}/check_privatedata`, null, { responseType: 'text' });
    }

    public unlockData(uniqueKey: String) {
        return this.httpClient.post(`${webServer}/unlock_privatedata`, { 'decryptionKey': uniqueKey }, { responseType: 'text' });
    }

    public newPrivateData(uniqueKey: String){
        return this.httpClient.post(`${webServer}/add_pubkey`, {'encryptionKey':uniqueKey}, { responseType: 'text' });
    }

    public reportUser() {
        return this.httpClient.post(`${webServer}/report_user`, null, { responseType: 'text' });
    }

}
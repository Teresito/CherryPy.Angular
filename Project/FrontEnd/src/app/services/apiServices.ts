import { HttpClient, HttpHeaders } from '@angular/common/http';
import { webServer } from '../constants';
import { Injectable } from '@angular/core';
import { componentState } from './componentService';

/* 
    COMPONENT FOR MAKING BACKEND/SERVER CALLS
*/
@Injectable()
export class apiServices {
    IP_LOCATION: any;

    constructor(private httpClient: HttpClient, private state: componentState) {
        this.IP_LOCATION = window.location.origin +"/client";
     }

    public async listUserAPI(): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/user_list`, {'username':sessionStorage.getItem('username')}, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION+'/user_list', {'username':sessionStorage.getItem('username')}, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response['userList'];
    }


    public loginAPI(user: String, pass: String) {
        // return this.httpClient.post(`${webServer}/login`, { "user": user, "pass": pass }, { responseType: 'json' }).toPromise();
        return this.httpClient.post(this.IP_LOCATION +'/login', { "user": user, "pass": pass }, { responseType: 'json' }).toPromise();
    }

    public async logoutAPI(): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/logout`, { 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +'/logout', { 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response;
    }

    public async checkPrivateData(): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/check_privatedata`, { 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +`/check_privatedata`, { 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response
    }

    public async unlockData(uniqueKey: String): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/unlock_privatedata`, { 'decryptionKey': uniqueKey, 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +`/unlock_privatedata`, { 'decryptionKey': uniqueKey, 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response
    }

    public async newPrivateData(uniqueKey: String): Promise<any>  {
        // let response = await this.httpClient.post(`${webServer}/add_pubkey`, { 'encryptionKey': uniqueKey, 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +`/add_pubkey`, { 'encryptionKey': uniqueKey, 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response;
    }

    public async reportUser(): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/report_user`, { 'username': sessionStorage.getItem('username'), 'userStatus': sessionStorage.getItem('status') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +`/report_user`, { 'username': sessionStorage.getItem('username'), 'userStatus': sessionStorage.getItem('status') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response;
    }

    public async broadcast(message: String): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/broadcast`, { 'message': message, 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +`/broadcast`, { 'message': message, 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response;
    }

    public async privatemessage(message: String, target_username: String, target_key: String): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/privateMessage`, { 'message': message, 'target_user':target_username,'target_key':target_key,'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +`/privateMessage`, { 'message': message, 'target_user':target_username,'target_key':target_key,'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response;
    }

    public async get_broadcastMessages(): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/get_publicMessages`, { 'username': sessionStorage.getItem('username') },{ responseType: 'json' }).toPromise()
        let response = await this.httpClient.post(this.IP_LOCATION +`/get_publicMessages`, { 'username': sessionStorage.getItem('username') },{ responseType: 'json' }).toPromise()
        this.checkResponse(response);
        return response['public_messages'];
    }

    public async get_privateMessages(): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/get_privateMessages`, { 'username': sessionStorage.getItem('username') },{ responseType: 'json' }).toPromise()
        let response = await this.httpClient.post(this.IP_LOCATION +`/get_privateMessages`, { 'username': sessionStorage.getItem('username') },{ responseType: 'json' }).toPromise()
        this.checkResponse(response);
        return response['private_messages'];
    }

    public async checkClients(): Promise<any> {
        // let response = await this.httpClient.post(`${webServer}/intervalCheck`, { 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        let response = await this.httpClient.post(this.IP_LOCATION +`/intervalCheck`, { 'username': sessionStorage.getItem('username') }, { responseType: 'json' }).toPromise();
        this.checkResponse(response);
        return response;
    }

    // CHECKS IF THE SERVER HAS THE USER LOGGED IN
    private checkResponse(response: any) {
        if (response == 2) {
            sessionStorage.setItem('badAccess',true.toString());
            this.state.clearClient();
        }
    }



}
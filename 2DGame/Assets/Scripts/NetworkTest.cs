using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;

public class NetworkTest : MonoBehaviour
{
    void Start()
    {
        // run tests
        if(NetworkManager._instance != null)
        {
            NetworkManager._instance.Send_CreateUser("test1");
            NetworkManager._instance.Send_PurchaseSword("test1");
            NetworkManager._instance.Send_PurchaseAxe("test1");
            NetworkManager._instance.Send_JoinGuild("test1", 1);
            NetworkManager._instance.Send_PlayerDeath("test1", 2,1,"axe",100,11);
        }
    }
}
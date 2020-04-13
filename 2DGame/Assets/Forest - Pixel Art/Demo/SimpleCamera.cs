using UnityEngine;
using System.Collections;

public class SimpleCamera : MonoBehaviour {

    private GameObject game_player;

    void Start()
    {
        game_player = CharacterManager._instance.playerObj;
    }

    // Update is called once per frame
    void Update () {
        transform.position = new Vector3(game_player.transform.position.x, 0, -10);
    }
}

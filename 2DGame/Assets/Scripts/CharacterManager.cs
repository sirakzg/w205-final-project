using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterManager : MonoBehaviour
{
    public GameObject playerObj;
    private int player_health = 10;
    private GameObject[] spawnedEnemies;

    public int current_weapon=0;
    public int current_guild=0;

    public GameObject[] sword_guilds;
    public GameObject[] axe_guilds;

    public GameObject[] enemies;


    public static CharacterManager _instance;
    private void Awake()
    {
        // enforce one instance of class per scene
        if (_instance == null)
            _instance = this;
        else return;

    }

    // Start is called before the first frame update
    void Start()
    {
        if (GameManager._instance.weaponType == 1)
            playerObj = GameObject.Instantiate(axe_guilds[GameManager._instance.guild], transform.position, Quaternion.identity, transform.parent);
        else
            playerObj = GameObject.Instantiate(sword_guilds[GameManager._instance.guild], transform.position, Quaternion.identity, transform.parent);

        playerObj.transform.localScale = new Vector3(0.5f,0.5f,0.5f);
        GameManager.PlayerHealthStatus(player_health);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0) && player_health > 0)
        {
            // Broadcast to nearby enemies of attack with position
            BroadcastMessage("PlayerAttacks", playerObj.transform.position.x, SendMessageOptions.DontRequireReceiver);
        }
    }

        public static float Distance2Player(Vector3 enemyLocal)
    {
        return _instance.playerObj.transform.position.x - enemyLocal.x;
    }

    public static void EnemeyAttacking(Vector3 enemyLocal)
    {
        if( Mathf.Abs(_instance.playerObj.transform.position.x - enemyLocal.x) < 0.64)
        {
            //Debug.LogError("Enemy Hit Player!");
            _instance.player_health--;
        }

        GameManager.PlayerHealthStatus(_instance.player_health);

        if (_instance.player_health == 0)
        {
            _instance.playerObj.GetComponent<Example_Motion_Attack_Shield_Controller>().PlayerKilledInAction();
        }
    }

}

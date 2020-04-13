using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    public int[] unlockTimes = new int[]{ 0,10,20,30,40,50};
    private float startTime = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        startTime = Time.time;
        StartCoroutine(SpawnAnEnemy());
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    IEnumerator SpawnAnEnemy()
    {
        while(true)
        {
            yield return new WaitForSeconds(Random.Range(1f,8f));

            // Use elapsed time to determine right enemy type to spawn based on unlock times
            int i;
            int elapsed = Mathf.RoundToInt( (Time.time - startTime) );
            for (i = unlockTimes.Length - 1; i > 0; i--)
                if (elapsed > unlockTimes[i])
                    break;

            GameObject spawn = GameObject.Instantiate(CharacterManager._instance.enemies[i], transform.position, Quaternion.identity, transform.parent);
            spawn.transform.localScale = Vector3.one;

            spawn.AddComponent<EnemyMoveAttack>();
        }
    }
}

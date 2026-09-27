PS C:\Users\PAULO TI\Desktop\MercadoDaBolaV2> git push
Enumerating objects: 13, done.
Counting objects: 100% (13/13), done.
Delta compression using up to 12 threads
Compressing objects: 100% (9/9), done.
Writing objects: 100% (9/9), 7.00 KiB | 1.75 MiB/s, done.
Total 9 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: 
remote: - GITHUB PUSH PROTECTION
remote:   —————————————————————————————————————————
remote:     Resolve the following violations before pushing again
remote: 
remote:     - Push cannot contain secrets
remote: 
remote:     
remote:      (?) Learn how to resolve a blocked push
remote:      https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line#resolving-a-blocked-push
remote:     
remote:     
remote:       —— Aiven Service Password ————————————————————————————
remote:        locations:
remote:          - commit: cc03c0298e28796c9197e8a56d7cc1f3d749341c
remote:            path: api.py:14
remote:          - commit: cc03c0298e28796c9197e8a56d7cc1f3d749341c
remote:            path: coletor_tm_tabelas.py:13
remote:          - commit: cc03c0298e28796c9197e8a56d7cc1f3d749341c
remote:            path: resetar_banco.py:11
remote:     
remote:        (?) To push, remove secret from commit(s) or follow this URL to allow the secret.
remote:        https://github.com/paulferreirac97-ops/MercadoDaBolaV2/security/secret-scanning/unblock-secret/3JvHuRuperbZF2hhwENr3skRCTh
remote:     
remote: 
remote: 
To https://github.com/paulferreirac97-ops/MercadoDaBolaV2.git
 ! [remote rejected] main -> main (push declined due to repository rule violations)
error: failed to push some refs to 'https://github.com/paulferreirac97-ops/MercadoDaBolaV2.git'
PS C:\Users\PAULO TI\Desktop\MercadoDaBolaV2> 
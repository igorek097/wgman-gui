from subprocess import run, PIPE


def generate_keys() -> dict:
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    preshared_key = generate_preshared_key()
    return {
        'public': public_key,
        'private': private_key,
        'preshared': preshared_key
    }


def generate_private_key() -> str:
    generate = run(['wg', 'genkey'], stdout=PIPE)
    return generate.stdout.decode().replace('\n', '')


def generate_public_key(private_key:str) -> str:
    generate = run(['echo', f'{private_key}'], stdout=PIPE)
    generate = run(['wg', 'pubkey'], input=generate.stdout, stdout=PIPE)
    return generate.stdout.decode().replace('\n', '')


def generate_preshared_key() -> str:
    generate = run(['wg', 'genpsk'], stdout=PIPE)
    return generate.stdout.decode().replace('\n', '')
if __name__ == '__main__':
    mu = 0.1
    epsilon = 5.
    w_clip = 0.1
    constant = 1.
    pattern_dp = "client_{}:" + f"\n\tnbafl:\n\t\tuse: True\n\t\tmu: {mu}\n\t\tepsilon: {epsilon}\n\t\tw_clip: {w_clip}\n\t\tconstant: {constant}\n".replace("\t", "  ")

    str_dp = ""
    delta = 5
    for n_clients in range(0, 100, delta):
        for inner_id in range(1, delta+1):
            client_id = n_clients + inner_id
            client_cfg = pattern_dp.format(client_id)
            str_dp += client_cfg

        with open(f'./{n_clients+delta:03}_clients.yaml', 'w') as f:
            f.write(str_dp)

use award::{get_wallet, init, Wallet};
use poc_framework_osec::{
    borsh::BorshDeserialize,
    solana_sdk::signature::{Keypair, Signer},
    Environment,
};

use sol_ctf_framework::ChallengeBuilder;

use solana_program::system_program;

use std::{
    error::Error,
    fs,
    io::Write,
    net::{TcpListener, TcpStream},
};

use threadpool::ThreadPool;

fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:5000")?;
    let pool = ThreadPool::new(4);
    for stream in listener.incoming() {
        let stream = stream.unwrap();
        println!("New Connection from: {}", stream.peer_addr().unwrap());
        pool.execute(|| {
            handle_connection(stream).unwrap();
        });
    }
    Ok(())
}

fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

    // load solve and chall programs
    let solve_pubkey = builder.input_program().unwrap();
    let program_pubkey = builder.chall_programs(&["./award.so"])[0];

    // make user
    let user = Keypair::new();

    writeln!(socket, "program pubkey: {}", program_pubkey)?;
    writeln!(socket, "solve pubkey: {}", solve_pubkey)?;
    writeln!(socket, "user pubkey: {}", user.pubkey())?;

    // add accounts and lamports
    let (wallet, _) = get_wallet(program_pubkey, user.pubkey());
    const INIT_BAL: u64 = 20_000;
    builder
        .builder
        .add_account_with_lamports(user.pubkey(), system_program::ID, INIT_BAL);

    let mut challenge = builder.build();

    // create a wallet
    challenge
        .env
        .execute_as_transaction(&[init(program_pubkey, user.pubkey())], &[&user]);

    // run solve
    challenge.input_instruction(solve_pubkey, &[&user]).unwrap();

    // check solve
    let wallet = challenge.env.get_account(wallet).unwrap();
    let wallet_data = Wallet::deserialize(&mut &wallet.data[..]).unwrap();
    writeln!(socket, "has_flag: {}", wallet_data.has_flag)?;

    if wallet_data.has_flag {
        let flag = fs::read_to_string("flag.txt").unwrap();
        writeln!(socket, "Congratulations! Here is your flag: {}", flag)?;
    } else {
        writeln!(socket, "flag: Sorry, you did not solve the challenge.")?;
    }

    Ok(())
}

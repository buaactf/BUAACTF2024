use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    msg,
    program::invoke_signed,
    pubkey::Pubkey,
    system_instruction,
};

use crate::{AwardInstruction, Wallet, WALLET_SIZE};

pub fn process_instruction(
    program: &Pubkey,
    accounts: &[AccountInfo],
    mut data: &[u8],
) -> ProgramResult {
    match AwardInstruction::deserialize(&mut data)? {
        AwardInstruction::Init { wallet_bump } => init(program, accounts, wallet_bump),
        AwardInstruction::Airdrop {} => airdrop(program, accounts),
        AwardInstruction::Buy {} => buy(program, accounts),
        AwardInstruction::Award {} => award(program, accounts),
    }
}

fn init(program: &Pubkey, accounts: &[AccountInfo], wallet_bump: u8) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let wallet = next_account_info(account_iter)?;
    let sys_prog = next_account_info(account_iter)?;

    let wallet_address = Pubkey::create_program_address(
        &["WALLET".as_bytes(), &user.key.to_bytes(), &[wallet_bump]],
        &program,
    )?;

    assert_eq!(*wallet.key, wallet_address);
    assert!(wallet.data_is_empty());
    assert!(user.is_signer);

    invoke_signed(
        &system_instruction::create_account(
            &user.key,
            &wallet_address,
            1,
            WALLET_SIZE as u64,
            &program,
        ),
        &[user.clone(), wallet.clone(), sys_prog.clone()],
        &[&["WALLET".as_bytes(), &user.key.to_bytes(), &[wallet_bump]]],
    )?;

    let wallet_data = Wallet {
        user: *user.key,
        amount: 0,
        claimed: false,
        has_award: false,
        has_flag: false,
        wallet_bump,
    };
    wallet_data
        .serialize(&mut &mut (*wallet.data).borrow_mut()[..])
        .unwrap();

    Ok(())
}

fn airdrop(program: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let wallet = next_account_info(account_iter)?;

    assert_eq!(wallet.owner, program);
    assert!(user.is_signer);
    let wallet_data = &mut Wallet::deserialize(&mut &(*wallet.data).borrow_mut()[..])?;
    assert_eq!(wallet_data.user, *user.key);

    if wallet_data.claimed {
        msg!("Already claimed");
    }

    wallet_data.amount += 25;
    wallet_data.claimed = true;
    wallet_data
        .serialize(&mut &mut (*wallet.data).borrow_mut()[..])
        .unwrap();
    Ok(())
}

fn buy(program: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let wallet = next_account_info(account_iter)?;

    assert_eq!(wallet.owner, program);
    assert!(user.is_signer);
    let wallet_data = &mut Wallet::deserialize(&mut &(*wallet.data).borrow_mut()[..])?;
    assert_eq!(wallet_data.user, *user.key);

    if wallet_data.amount >= 10 {
        wallet_data.amount -= 15;
        wallet_data.has_award = true;
    } else {
        msg!("Not enough funds");
    }
    wallet_data
        .serialize(&mut &mut (*wallet.data).borrow_mut()[..])
        .unwrap();
    Ok(())
}

fn award(program: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let wallet = next_account_info(account_iter)?;

    assert_eq!(wallet.owner, program);
    assert!(user.is_signer);
    let wallet_data = &mut Wallet::deserialize(&mut &(*wallet.data).borrow_mut()[..])?;
    assert_eq!(wallet_data.user, *user.key);

    if wallet_data.amount >= 100 && wallet_data.has_award == true {
        wallet_data.has_flag = true;
    } else {
        msg!("Not enough funds or no award");
    }

    wallet_data
        .serialize(&mut &mut (*wallet.data).borrow_mut()[..])
        .unwrap();
    Ok(())
}

mod entrypoint;
pub mod processor;

use std::mem::size_of;

use borsh::{BorshDeserialize, BorshSerialize};

use solana_program::{
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    system_program,
};

#[derive(BorshSerialize, BorshDeserialize)]
pub enum AwardInstruction {
    Init { wallet_bump: u8 },
    Airdrop {},
    Buy {},
    Award {},
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Wallet {
    pub user: Pubkey,
    pub amount: u8,
    pub claimed: bool,
    pub has_award: bool,
    pub has_flag: bool,
    pub wallet_bump: u8,
}

pub const WALLET_SIZE: usize = size_of::<Wallet>();

pub fn get_wallet(program_id: Pubkey, user: Pubkey) -> (Pubkey, u8) {
    Pubkey::find_program_address(&["WALLET".as_bytes(), &user.to_bytes()], &program_id)
}

pub fn init(program: Pubkey, user: Pubkey) -> Instruction {
    let (wallet, wallet_bump) = get_wallet(program, user);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(wallet, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: AwardInstruction::Init { wallet_bump }.try_to_vec().unwrap(),
    }
}

pub fn airdrop(program: Pubkey, user: Pubkey) -> Instruction {
    let (wallet, _) = get_wallet(program, user);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(wallet, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: AwardInstruction::Airdrop {}.try_to_vec().unwrap(),
    }
}

pub fn buy(program: Pubkey, user: Pubkey) -> Instruction {
    let (wallet, _) = get_wallet(program, user);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(wallet, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: AwardInstruction::Buy {}.try_to_vec().unwrap(),
    }
}

pub fn award(program: Pubkey, user: Pubkey) -> Instruction {
    let (wallet, _) = get_wallet(program, user);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(wallet, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: AwardInstruction::Award {}.try_to_vec().unwrap(),
    }
}

import React from 'react'
import ReactModal from 'react-modal';

interface HouseholdJoinModalProps{
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>
  household_id: string;
  household_name: string;
}

const HouseholdJoinModal = ({isOpen, setIsOpen, household_id, household_name}: HouseholdJoinModalProps) => {
  const close_modal = () => {
    setIsOpen(false)
  }
  
    return (
    <ReactModal isOpen={isOpen} onRequestClose={close_modal}>
      <div>{household_id}</div>
      <div>{household_name}</div>
      <input type="button" value="Confirm"></input>
    </ReactModal>
  )
}

export default HouseholdJoinModal
import React from 'react'
import ReactModal from 'react-modal';

interface HouseholdJoinModalProps{
  isOpen: boolean;
  household_id: string;
  household_name: string;
}

const HouseholdJoinModal = ({isOpen, household_id, household_name}: HouseholdJoinModalProps) => {
  return (
    <ReactModal isOpen={isOpen}>
      <div>{household_id}</div>
      <div>{household_name}</div>
      <input type="button">Confirm</input>
    </ReactModal>
  )
}

export default HouseholdJoinModal
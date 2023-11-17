interface UploadTileProps{
    colour: string
}


const UploadTile = ({colour}: UploadTileProps) => {
  return (
    <div className={"upload_tile " + colour}></div>
  )
}

export default UploadTile
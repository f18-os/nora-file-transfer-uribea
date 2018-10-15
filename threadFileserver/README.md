# File transfer server
tcp file transfer from client to server

This program consist of two programs

* threadFileServer     
    *  thread to handle multiple simultaneaous clients
    * opens file in server directory and writes to it
    * line 50 of threadFileServer can be changed to different directories
    

* threadFileClient
    * To use: "put [filename]"
    * Can connect to fileServer with or without the stammerProxy
    * Zero length files
        * write empty file in server
    * File doesn't exist
        * exits without writing
        * prints file not found
    * file already on server
        * overwrites file on server


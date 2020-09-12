// Jacob Lucke

#include <stdio.h>
#include <iostream>
#include <fcntl.h>
#include <sys/stat.h>
#include <curl/curl.h>
#include <string>

void performRequest(std::string request, char *file, char *url)
{
  CURL *curl; // curl handle
	CURLcode returnCode;
	struct stat file_info;
  FILE * fileptr;
  long httpcode;

  stat(file, &file_info);
  fileptr = fopen(file, "rb");

  curl = curl_easy_init();
  
  if (curl)
  {
    curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);

    if (request.compare("PUT") == 0)
    {
      std::cout << "Specified: PUT" << std::endl;
      curl_easy_setopt(curl, CURLOPT_PUT, 1L);
    }
    else if (request.compare("POST") == 0)
    {
      std::cout << "Specified: POST" << std::endl;
      curl_easy_setopt(curl, CURLOPT_POST, 1L);
    }
    else
    {
      fprintf(stderr, "PUT or POST are allowed for the second argument.\n");
      curl_easy_cleanup(curl);
      fclose(fileptr);
      return;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);

    curl_easy_setopt(curl, CURLOPT_READDATA, fileptr);

    curl_easy_setopt(curl, CURLOPT_INFILESIZE_LARGE, (curl_off_t)file_info.st_size);

    curl_easy_setopt(curl, CURLOPT_FAILONERROR, 1L);

    curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    returnCode = curl_easy_perform(curl);

    if(returnCode == CURLE_HTTP_RETURNED_ERROR)
    {
      curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpcode);
      fprintf(stderr, "curl_easy_perform() failed with HTTP status: %ld\n", httpcode);
    }

    curl_easy_cleanup(curl);
  }

  fclose(fileptr);
}

int main(int argc, char **argv)
{
  std::string request;
  char *file;
  char *url;
 
  if(argc < 4)
    return 1;
  
  request = argv[1];
  file = argv[2];
  url = argv[3];

  std::cout << "file: " << file << std::endl;
  std::cout << "url: " << url << std::endl;
 
  curl_global_init(CURL_GLOBAL_ALL);

  performRequest(request, file, url);

  curl_global_cleanup();
  return 0;
}
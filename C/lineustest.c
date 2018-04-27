/*
 *    lineustest - plot a path on the line-us plotter
 *
 *              paul haeberli - 2018
 *
 *    based on an excellent answer by Ciro Santilli on stackoverflow:
 *        https://stackoverflow.com/questions/307692/simplest-way-to-open-and-use-a-socket-in-c
 *
 *    Ciro's code also on github:
 *        https://github.com/cirosantilli/cpp-cheat
 *
 */
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <math.h>

#define MIN_X           ( 700)
#define MAX_X           (1800)
#define MIN_Y           (-700)
#define MAX_Y           ( 700)
#define RANGE_X         (MAX_X-MIN_X)
#define RANGE_Y         (MAX_Y-MIN_Y)
#define CENTER_X        ((MAX_X+MIN_X)/2)
#define CENTER_Y        ((MAX_Y+MIN_Y)/2)

static char buffer[BUFSIZ];
static int sockfd;

void send_command(char *str)
{
    int str_len = strlen(str);
    if (write(sockfd, str, str_len+1) == -1) {
        perror("write");
        exit(EXIT_FAILURE);
    }
}

void read_response(int echo)
{
    ssize_t nbytes_read;

    if ((nbytes_read = read(sockfd, buffer, BUFSIZ)) > 0) {
        if(echo) {
            write(STDOUT_FILENO, buffer, nbytes_read);
            if (buffer[nbytes_read - 1] == '\n')
                fflush(stdout);
        }
    }
}

void init()
{
    char protoname[] = "tcp";
    struct protoent *protoent;
    in_addr_t in_addr;
    struct hostent *hostent;
    struct sockaddr_in sockaddr_in;
    char *server_hostname = "line-us.local";
    unsigned short server_port = 1337;

    protoent = getprotobyname(protoname);
    if (protoent == NULL) {
        perror("getprotobyname");
        exit(EXIT_FAILURE);
    }
    sockfd = socket(AF_INET, SOCK_STREAM, protoent->p_proto);
    if (sockfd == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    /* Prepare sockaddr_in. */
    hostent = gethostbyname(server_hostname);
    if (hostent == NULL) {
        fprintf(stderr, "error: gethostbyname(\"%s\")\n", server_hostname);
        exit(EXIT_FAILURE);
    }
    in_addr = inet_addr(inet_ntoa(*(struct in_addr*)*(hostent->h_addr_list)));
    if (in_addr == (in_addr_t)-1) {
        fprintf(stderr, "error: inet_addr(\"%s\")\n", *(hostent->h_addr_list));
        exit(EXIT_FAILURE);
    }
    sockaddr_in.sin_addr.s_addr = in_addr;
    sockaddr_in.sin_family = AF_INET;
    sockaddr_in.sin_port = htons(server_port);

    /* Do the actual connection. */
    if (connect(sockfd, (struct sockaddr*)&sockaddr_in, sizeof(sockaddr_in)) == -1) {
        perror("connect");
        exit(EXIT_FAILURE);
    }

    read_response(1);
}

/* gcode functions */

void gcode_setpen(int z)
{
    char send_buffer[BUFSIZ];
    sprintf(send_buffer, "G01 Z%d", z);
    send_command(send_buffer);
    read_response(0);
}

void gcode_movexy(int x, int y)
{
    char send_buffer[BUFSIZ];
    sprintf(send_buffer, "G01 X%d Y%d", x, y);
    send_command(send_buffer);
    read_response(0);
}

/* drawing functions */

int pendown = 0;

void moveto(float x, float y)
{
    if(pendown) {
        gcode_setpen(1000);
        pendown = false;
    }
    gcode_movexy(round(x), round(y));
}

void lineto(float x, float y)
{
    if(!pendown) {
        gcode_setpen(0);
        pendown = true;
    }
    gcode_movexy(round(x), round(y));
}

void drawrect(float orgx, float orgy, float sizex, float sizey)
{
    moveto(orgx      , orgy      );
    lineto(orgx+sizex, orgy      );
    lineto(orgx+sizex, orgy+sizey);
    lineto(orgx      , orgy+sizey);
    lineto(orgx      , orgy      );
}

#define MIN_STEP        ((2.0*M_PI)/6.0)

void spiral(float orgx, float orgy, float radius)
{
    moveto(orgx,orgy);
    double ntimes = radius/25;
    double da = 2*M_PI/10;
    for(double around=0.01; around<ntimes; around+=da) {
        double r = around*radius/ntimes;
        double a = 2.0*M_PI*around;
        lineto(orgx+r*cos(a), orgy+r*sin(a));
        da = 10.0/r;
        if(da>MIN_STEP)
            da=MIN_STEP;
    }
}

int main(int argc, char **argv) 
{
    if(argc != 1) {
        fprintf(stderr, "usage: lineustest\n");
        exit(1);
    }

    init();

    drawrect(MIN_X, MIN_Y, RANGE_X, RANGE_Y);
    spiral(CENTER_X, CENTER_Y, 0.48*RANGE_X);

    return 0;
}

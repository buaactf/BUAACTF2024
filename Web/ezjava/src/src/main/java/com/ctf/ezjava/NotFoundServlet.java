package com.ctf.ezjava;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name="NotFoundServlet", urlPatterns="/notFound")
public class NotFoundServlet extends HttpServlet {
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        response.setCharacterEncoding("UTF-8");
        response.setStatus(HttpServletResponse.SC_NOT_FOUND);
        response.getWriter().write("<html><head><title>404 Not Found</title></head><body>");
        response.getWriter().write("<h1>404 Not Found</h1>");
        response.getWriter().write("<p>The requested URL " + request.getRequestURI() + " was not found on this server.</p>");
        response.getWriter().write("</body></html>");
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        doGet(request, response);
    }
}

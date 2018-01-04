(ql:quickload :miscoined)

(defpackage miscoined.app
  (:use :cl)
  (:import-from :lack.builder
                :builder)
  (:import-from :ppcre
                :scan)
  (:import-from :miscoined.web
                :*web*)
  (:import-from :miscoined.config
                :config
                :productionp
                :*static-directory*))
(in-package :miscoined.app)

(builder
 (:static
  :path (lambda (path)
          (when (ppcre:scan
                 "^(?:/docs/|/fonts/|/images/|/css/|/js/|/robot\\.txt$|/favicon\\.ico$)"
                 path)
            path))
  :root *static-directory*)
 (unless (productionp)
   :accesslog)
 (when (getf (config) :error-log)
   `(:backtrace
     :output ,(getf (config) :error-log)))
 :session
 (unless (productionp)
   (lambda (app)
     (lambda (env)
       (funcall app env))))
 *web*)
